import torch
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

# Load .chk file
def load_checkpoint(file_path):
    """
    Load a checkpoint file and return its contents.

    Args:
        file_path (str): Path to the .chk file.

    Returns:
        dict: A dictionary containing the checkpoint data.
    """
    checkpoint = torch.load(file_path, map_location=torch.device('cpu'), weights_only=False)
    print(f"Loaded checkpoint from: {file_path}")
    print(f"Epoch: {checkpoint['epoch']}, Learning Rate: {checkpoint['lr']}")
    return checkpoint


# Load TensorBoard events
def read_tensorboard_logs(log_dir):
    """
    Read TensorBoard logs and extract scalar data.

    Args:
        log_dir (str): Path to the directory containing TensorBoard logs.

    Returns:
        dict: A dictionary with scalar data (e.g., training and validation losses).
    """
    event_acc = EventAccumulator(log_dir)
    event_acc.Reload()

    # Extract scalar data
    scalar_data = {}
    for tag in event_acc.Tags()['scalars']:
        scalar_data[tag] = [(scalar.step, scalar.value) for scalar in event_acc.Scalars(tag)]
    
    print(f"Extracted data from TensorBoard logs in: {log_dir}")
    return scalar_data