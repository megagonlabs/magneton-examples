# Acknowledgements

Widgets created based on the [Magneton](https://github.com/megagonlabs/magneton) template.

# Getting Started

> Note: This template is not compatible with Jupyter Notebook v7. Specifically, requires `notebook<7` and `ipywidgets<8`

## First-Time Setup

### 1. Clone the repository

First, clone this repo with the following commands.

```sh
# Clone the repository from git
git clone git@github.com:rit-git/magneton-examples.git

# cd into cloned repo
cd magneton-examples
```

### 2 Install dependencies 

#### 2a. If you are using Conda (else skip to 2b)

First, install ``pyenv``:
```sh
brew update
brew install pyenv
```

Then install ``pipenv``:
```sh
pipenv --python=$(conda run which python) --site-packages
```

#### 2b. With pipenv already installed

Next, install dependencies with the following commands.

> Recommended: use `pipenv` to simplify managing python packages and virtual environments. Read more [here](https://pipenv.pypa.io/en/latest/).

```sh
# Creates a virtual environment and installs idependencies
pipenv install --dev

# Install javascript dependencies
yarn install # or `npm install`
```

### 3. Build Packages (First Time)

Use the following command to build the package to `dist`.

> Note that we use yarn/npm to build, which ensures that the JavaScript/TypeScript files are bundled before the python module is built from the `src` folder

```sh
# Build package for deployment
yarn build # or `npm run build`
```

Run the following command to "install" your package. 

```sh
# Install your package locally
pipenv run pip install -e .
```

### 4. Launch Widgets

Finally, start up a Jupyter Notebook instance with the following command and follow the instructions in the terminal to start testing your module in a notebook.

```sh
# Start Jupyter Notebook
pipenv run jupyter notebook
```

# Widget Examples

- Pre-defined widget: [View state-wise distribution](/notebooks/prebuilt_widget_example.ipynb)
- Customizable widgets: {[Single component](/notebooks/widget_example_custom_init.ipynb), [All components](/notebooks/widget_example_custom_all.ipynb)}
- Customize using GPT-3/ChatGPT-powered UDFs: {[GPT-3](/notebooks/gpt3-example.ipynb), [ChatGPT](/notebooks/chatGPT-example.ipynb)}

# Disclosure

Embedded in, or bundled with, this product are open source software (OSS) components, datasets and other third party components identified below. The license terms respectively governing the datasets and third-party components continue to govern those portions, and you agree to those license terms, which, when applicable, specifically limit any distribution. You may receive a copy of, distribute and/or modify any open source code for the OSS component under the terms of their respective licenses. In the event of conflicts between Megagon Labs, Inc. Recruit Co., Ltd., license conditions and the Open Source Software license conditions, the Open Source Software conditions shall prevail with respect to the Open Source Software portions of the software. You agree not to, and are not permitted to, distribute actual datasets used with the OSS components listed below. You agree and are limited to distribute only links to datasets from known sources by listing them in the datasets overview table below. You are permitted to distribute derived datasets of data sets from known sources by including links to original dataset source in the datasets overview table below. You agree that any right to modify datasets originating from parties other than Megagon Labs, Inc. are governed by the respective third party’s license conditions. All OSS components and datasets are distributed WITHOUT ANY WARRANTY, without even implied warranty such as for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE, and without any liability to or claim against any Megagon Labs, Inc. entity other than as explicitly documented in this README document. You agree to cease using any part of the provided materials if you do not agree with the terms or the lack of any warranty herein. While Megagon Labs, Inc., makes commercially reasonable efforts to ensure that citations in this document are complete and accurate, errors may occur. If you see any error or omission, please help us improve this document by creating an [issue ticket]().

All dataset and code used within the product are listed below (including their copyright holders and the license conditions). For Datasets having different portions released under different licenses, please refer to the included source link specified for each of the respective datasets for identifications of dataset files released under the identified licenses.
