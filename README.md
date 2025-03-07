# hcptrt.paper

Welcome to **hcptrt.paper**, the slickest datapaper repo around. Buckle up! 🚀

## Repository Structure

```
.
├── README.md         # You're looking at it. Behold. 📖
├── myst_article      # The reproducible magic behind the paper ✨
├── sourcedata        # Data and analyses assets 📊
├── src               # Custom modules to make numbers dance 🕺
├── containers        # Apptainer build files & images—because environments matter 🛠️
├── tasks.py          # Invoke automation wizardry 🧙‍♂️
├── requirements.txt  # Bare-minimum Python dependencies 📦
└── requirements_dev.txt # Extra goodies for Jupyter Lab devs 💻
```

## Installation

## Development

Want to keep things clean? I suggest working in a `virtualenv` environment. 🧼

To install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

Need a Jupyter Lab setup to hack away in style, using open-source community-driven libraries? 🚀

```bash
pip install -r requirements_dev.txt
```

And you're done! It's enough to work on the project, and in particular contribute to the notebooks in the `myst_article` folder. 🎯

## MyST Reproducible Article

If you want to take things to the next level 🚀 and run a set of fully reproducible analyses, you'll need [Apptainer](https://apptainer.org/) and [MyST-MD](https://mystmd.org/). But don't worry, it will go smoothly. 😎

### Container Generation

Let’s first set up the containerized environment. Make sure [Apptainer](https://apptainer.org/docs/admin/main/installation.html) is installed. If you're on Debian, check out [this guide](https://apptainer.org/docs/admin/main/installation.html#install-debian-packages).

To create an image for your container:

```bash
invoke container-build
```

### Live View of the Article

Once the container is successfully generated, you can see the article in action! Run this bad boy: 🔥

```bash
invoke article
```

Need to **fully re-run** all notebooks before previewing for a clean, reproducible execution? 🔄

```bash
invoke article --execute
```

MyST has smart caching—only changed notebooks rerun. But if you like things completely fresh, start by running before generating the live view:

```bash
invoke article-clean
```

### Static HTML Generation

A live article is cool, but a **static HTML** version is perfect for sharing as a website. 🌐

To generate it:

```bash
invoke html-build
```

Need a fresh build with all notebooks re-executed? 🛠️

```bash
invoke html-build --execute
```

Deploying to GitHub Pages? You'll want a base URL: 🔗

```bash
invoke html-build --execute --base-url "hcptrt.paper/"
```

Want to serve the HTML locally just to check? 👀

```bash
invoke html-serve
```

### Publishing to GitHub Pages

Got your GitHub Pages set up? Just run: 🚀

```bash
invoke html-publish
```

Boom. Your article is live! 🎉
