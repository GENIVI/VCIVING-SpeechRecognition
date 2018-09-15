This is the emulation core of Voice Command of IVI System.
This runs only on PCs.

In order to make use of DeepSpeech,
1. Download and extract the pre-trained model files as follows.
    ```bash
    wget -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz | tar xvfz -
    ```
2. Change the following values in [settings.json](settings.json) considering the files downloaded and extracted above.
    * sr_model_file_path : Path to the file ending with the extension .pb.
    * sr_alphabet_file_path: Path to the .txt file(usually named as alphabet.txt)
    * sr_lm_file_path: Path to the binary file in the archive(Usually called lm.binary)
    * sr_trie_file_path: Path to the file without extensions(Usually named as trie)
    
3. If you have GPU support on your platform/device, please consider installing deepspeech-gpu package. Checkout the instructions at [DeepSpeech Repository](https://github.com/mozilla/DeepSpeech). Otherwise, please continue with the installation instructions on your platform. That would fetch the required deepspeech package.