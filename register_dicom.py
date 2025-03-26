import os
import pydicom
import SimpleITK as sitk
import ants
import time

def load_dicom_series(directory):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directory)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    return image


def register_images(fixed_image, moving_image, output_dir):
    # Convert SimpleITK images to ANTs images
    fixed = ants.from_numpy(sitk.GetArrayFromImage(fixed_image))
    moving = ants.from_numpy(sitk.GetArrayFromImage(moving_image))

    # Perform registration using ANTs
    registration = ants.registration(fixed, moving, type_of_transform='SyN')

    # Convert the registered image back to SimpleITK
    registered_image = sitk.GetImageFromArray(registration['warpedmovout'].numpy())
    registered_image.CopyInformation(fixed_image)

    # Save the registered image
    sitk.WriteImage(registered_image, os.path.join(output_dir, 'registered_image.nii'))

    return registered_image


def main():
    base_dir = 'Qian Xinmei'
    intraoperative_dirs = ['intraoperative/axial', 'intraoperative/coronal', 'intraoperative/sagittal']
    preoperative_dirs = ['preoperative/axial', 'preoperative/coronal', 'preoperative/sagittal']

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    print('Start registration...\n')
    start_time = time.time()  # Correct time calculation
    for intra_dir, pre_dir in zip(intraoperative_dirs, preoperative_dirs):
        intra_path = os.path.join(base_dir, intra_dir)
        pre_path = os.path.join(base_dir, pre_dir)

        fixed_image = load_dicom_series(pre_path)
        moving_image = load_dicom_series(intra_path)

        if fixed_image is None or moving_image is None:
            print(f"Skipping registration for {intra_dir} to {pre_dir} due to non-uniform sampling or missing slices.")
            continue

    registered_image = register_images(fixed_image, moving_image, output_dir)
    print(f'Registered {intra_dir} to {pre_dir} and saved to {output_dir}')
    end_time = time.time()
    print('Time used :', end_time - start_time)


if __name__ == '__main__':
    main()

