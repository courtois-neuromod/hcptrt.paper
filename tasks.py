from invoke import task
import os

CONTAINER_PATH = "container/container-myst.sif"
CONTAINER_NAME = "hcptrt.paper_container"
DEFINITION_FILE = "container/container-myst.def"

@task
def container_build(c):
    """Build (or rebuild) the Apptainer container from myst.def."""
    print("🚀 Building the Apptainer container...")

    # Ensure container directory exists
    os.makedirs("container", exist_ok=True)

    # Force rebuild the container
    c.run(f"apptainer build --force {CONTAINER_PATH} {DEFINITION_FILE}")

    print("✅ Container built successfully!")

@task

def container_start(c):
    """Start a persistent Apptainer container (if not already running)."""
    print("🚀 Starting MyST container in the background...")

    # Check if container is already running
    result = c.run(f"apptainer instance list | grep {CONTAINER_NAME}", warn=True, hide=True)

    if result.ok:
        print(f"✅ Container '{CONTAINER_NAME}' is already running.")
    else:
        # Start the container as an instance
        c.run(f"apptainer shell --bind $PWD:/workspace {CONTAINER_PATH} {CONTAINER_NAME}")
        print(f"✅ Container '{CONTAINER_NAME}' started!")

@task
def container_stop(c):
    """Stop the persistent Apptainer container."""
    print("🛑 Stopping MyST container...")
    c.run(f"apptainer instance stop {CONTAINER_NAME}")
    print("✅ Container stopped.")

@task
def paper(c):
    """Start MyST paper server locally (Live Preview)."""
    print("📖 Starting live MyST paper server on http://localhost:3000...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke create_container` first.")
        return

    c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} myst start", pty=True)

    print("✅ MyST live paper is running!")

@task
def paper_clean(c):
    """Clean the built paper files using MyST's built-in clean command."""
    print("🧹 Cleaning up built paper...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke build_container` first.")
        return

    # Run MyST's built-in clean command
    c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} myst clean")

    print("✅ paper build cleaned!")

@task
def html_build(c, base_url=None):
    """Build static HTML documentation (for deployment)."""
    print("📝 Building static HTML docs...")

    if not os.path.exists(CONTAINER_PATH):
        print("❌ Container image not found. Run `invoke build_container` first.")
        return

    # Determine BASE_URL
    html_path = os.path.abspath("_build/html/")
    html_index = os.path.join(html_path, "index.html")

    # Build static HTML docs with BASE_URL set
    if base_url:
        c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} env BASE_URL={base_url} myst build --html")
    else:
        c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} myst build --html")

    if os.path.exists(html_index):
        print(f"✅ Static HTML docs successfully generated! Open: \033[94mfile://{html_index}\033[0m")
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
    c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} http-server /workspace/_build/html -p 3000", pty=True)

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
    c.run(f"apptainer exec --bind $PWD:/workspace {CONTAINER_PATH} ghp-import -n -p -f /workspace/_build/html")

    print("✅ Docs successfully published to GitHub Pages!")
