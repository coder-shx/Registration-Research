import nibabel as nib
import matplotlib.pyplot as plt

def display_slice(slice):
    plt.imshow(slice.T, cmap="gray", origin="lower")
    plt.show()

def main():
    # Load the .nii file
    nii_file = 'output/registered_image.nii'
    img = nib.load(nii_file)
    data = img.get_fdata()

    # Display all slices,change the parameter to display different slices
    for i in range(data.shape[2]):
        display_slice(data[:, :, i])

if __name__ == "__main__":
    main()
