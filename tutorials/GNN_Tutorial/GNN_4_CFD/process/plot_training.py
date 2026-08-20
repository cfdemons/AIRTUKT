import matplotlib.pyplot as plt

# Plot the training and validation losses againt epochs
def plot_losses(tensorboard_data):
    """
    Plot training and validation losses from TensorBoard data.

    Args:
        tensorboard_data (dict): Dictionary containing scalar data from TensorBoard.
    """
    if 'Loss/train' in tensorboard_data and 'Loss/test' in tensorboard_data:
        train_steps, train_losses = zip(*tensorboard_data['Loss/train'])
        test_steps, test_losses = zip(*tensorboard_data['Loss/test'])

        plt.figure(figsize=(10, 5))
        plt.plot(train_steps, train_losses, label='Training Loss', color='blue')
        plt.plot(test_steps, test_losses, label='Validation Loss', color='orange')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.title('Training and Validation Losses')
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("No training or validation loss data available for plotting.")


def plot_lr(chk_data):
    """
    Plot learning rate from checkpoint data.

    Args:
        .chk file (dict): Dictionary containing scalar data from .chk file.
    """
    print('a')
    if 'lr' in chk_data and 'epoch' in chk_data:
        epochs = chk_data['epoch']
        lrs = chk_data['lr']
        
        plt.figure(figsize=(10, 5))
        plt.plot(epochs, lrs, label='Learning Rate', color='green')
        plt.xlabel('Epochs')
        plt.ylabel('Learning Rate')
        plt.title('Learning Rate v Epochs')
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("No learning rate data available for plotting.")