"""
Train CNN model on DFU (Diabetic Foot Ulcer) dataset.
Uses the Patches data from USE CASE 02:
  - datasets/images/normal/    (544 images)
  - datasets/images/ulcers/    (513 images)
"""

import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import time


# Add backend to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ml.cnn_model import create_model
from app.ml.dataset_loader import UlcerDataset


def train():
    # --- Config ---
    DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "images")
    MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "models")
    EPOCHS = 15
    BATCH_SIZE = 16
    LEARNING_RATE = 0.0003
    TEST_SPLIT = 0.2
    PATIENCE = 5  # Early stopping patience

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # --- Load Dataset ---
    print(f"Loading dataset from: {DATASET_PATH}")
    dataset = UlcerDataset(DATASET_PATH)
    print(f"Total images: {len(dataset)} (normal=0, ulcer=1)")

    if len(dataset) == 0:
        print("ERROR: No images found. Check that datasets/images/normal/ and datasets/images/ulcers/ exist.")
        return

    # Split into train and validation
    total = len(dataset)
    val_size = int(total * TEST_SPLIT)
    train_size = total - val_size

    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    print(f"Train: {train_size}, Validation: {val_size}")

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # --- Create Model ---
    model = create_model(num_classes=2, pretrained=True)
    model = model.to(device)
    print("Model: ResNet18 (pretrained) with 2-class head")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.1, patience=3)

    # --- Training Loop ---
    best_accuracy = 0.0
    patience_counter = 0
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

    print(f"\nStarting training for {EPOCHS} epochs...")
    print("-" * 60)

    for epoch in range(EPOCHS):
        start_time = time.time()

        # Train
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()

        train_loss /= len(train_loader)
        train_acc = 100.0 * train_correct / train_total

        # Validate
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_loss /= len(val_loader)
        val_acc = 100.0 * val_correct / val_total

        scheduler.step(val_loss)

        elapsed = time.time() - start_time

        print(
            f"Epoch [{epoch+1:2d}/{EPOCHS}] "
            f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.1f}% | "
            f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.1f}% | "
            f"Time: {elapsed:.1f}s"
        )

        # Save best model and check early stopping
        if val_acc > best_accuracy:
            best_accuracy = val_acc
            save_path = os.path.join(MODEL_SAVE_PATH, "best_dfu_model.pth")
            torch.save(model.state_dict(), save_path)
            print(f"  -> Saved best model (val_acc={val_acc:.1f}%)")
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f"Early stopping at epoch {epoch+1} (no improvement for {PATIENCE} epochs)")
                break

    print("-" * 60)
    print(f"Training complete! Best validation accuracy: {best_accuracy:.1f}%")
    print(f"Model saved to: {os.path.join(MODEL_SAVE_PATH, 'best_dfu_model.pth')}")


if __name__ == "__main__":
    train()
