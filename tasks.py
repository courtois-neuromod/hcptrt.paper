from invoke import task
import os

MYST_PATH = "myst_article"
CONTAINER_PATH = "containers/myst.sif"
CONTAINER_NAME = "hcptrt.myst_article_container"
DEFINITION_FILE = "containers/myst.def"

@task
def container_build(c):
    """Build (or rebuild) the Apptainer container from myst.def."""
    print("🚀 Building the Apptainer container...")

    # Force rebuild the container
    c.run(f"apptainer build --force {CONTAINER_PATH} {DEFINITION_FILE}")

    print("✅ Container built successfully!")

@task
def article(c, execute=False):
    """Start MyST article server locally (Live Preview)."""
    print("📖 Starting live MyST article server on http://localhost:3000...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke create_container` first.")
        return

    if not os.path.exists(MYST_PATH):
        print(f"❌ Myst article path not found: {MYST_PATH}. Try editing MYST_PATH in tasks.py")
        return

    # Conditionally add "--execute" flag
    execute_flag = "--execute" if execute else ""
    c.run(f"apptainer exec --bind {MYST_PATH}:/workspace {CONTAINER_PATH} bash -c 'cd /workspace && myst start {execute_flag}'", pty=True)

    print("✅ MyST live article is running!")

@task
def article_clean(c):
    """Clean the built article files using MyST's built-in clean command."""
    print("🧹 Cleaning up built article...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke build_container` first.")
        return

    # Run MyST's built-in clean command
    c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} myst clean")

    print("✅ article build cleaned!")

@task
def html_build(c, base_url=None, execute=False):
    """Build static HTML documentation (for deployment)."""
    print("📝 Building static HTML docs...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke build_container` first.")
        return

    # Determine BASE_URL
    html_path = os.path.join(f"{MYST_PATH}", "_build/html/")
    html_index = os.path.join(html_path, "index.html")

    # Conditionally add "--execute" flag
    execute_flag = "--execute" if execute else ""

    # Conditionally add a base_url to the build
    base_url_flag = f"env BASE_URL={base_url} &&" if base_url else ""


    # Build static HTML docs with BASE_URL set
    c.run(f"apptainer exec --bind {MYST_PATH}:/workspace {CONTAINER_PATH} bash -c 'cd /workspace && {base_url_flag} myst build --html {execute_flag}'")

    if os.path.exists(html_index):
        print(f"✅ Static HTML docs successfully generated! use `invoke html-serve` to explore the site")
    else:
        print("❌ Build failed! Check the logs for errors.")

@task
def html_serve(c):
    """Serve the built HTML documentation from inside the container."""
    print("🌍 Serving static HTML docs on http://localhost:3000...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke build_container` first.")
        return

    # Start the HTTP server inside Apptainer
    c.run(f"apptainer exec --bind {MYST_PATH}:/workspace {CONTAINER_PATH} http-server /workspace/_build/html -p 3000", pty=True)

@task
def html_publish(c):
    """Publish the static HTML docs to the GitHub Pages branch."""
    print("🚀 Publishing HTML docs to GitHub Pages...")

    # Ensure build exists
    html_path = os.path.abspath("_build/html/")
    if not os.path.exists(html_path):
        print("❌ No built HTML docs found. Run `invoke docs_html` first.")
        return

    # Run ghp-import inside the container
    c.run(f"apptainer exec --bind {MYST_PATH}:/workspace {CONTAINER_PATH} ghp-import -n -p -f /workspace/_build/html")

    print("✅ Docs successfully published to GitHub Pages!")
