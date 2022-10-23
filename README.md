# <a><img alt="StreamerInfo logo" src="static/logo_icon.png" width="64" height="64"></a> StreamerInfo

> StreamerInfo serves dynamically generated illustrations containing current information about a streamers stream status (Twitch only).

## Changelog
> You can find the current changelog of released and unreleased features in the [CHANGELOG.md](CHANGELOG.md) file. 

## Installation
> **Prerequisites & Dependencies**<br>
> OS: `Windows 7+, macOS 11+, Debian 10+`<br>
> Architecture: `64 bit`<br>
> **Optional <small>(when directly running the sourcecode or building for Windows)</small>**<br>
> Runtime: `Python 3.10+`<br>
> Build environment: `MSYS2`
- Download latest stable binaries from <https://github.com/noecosta/StreamerInfo/releases>
- Run `StreamerInfo.exe / StreamerInfo` in the main directory (where the downloaded binaries lie)

## Development
> The following setup is required to initialize this project.
```shell
# requirement: installed version of Python 3.10+, run all of those commands in the root directory of this project
# install virtualenv module
pip install virtualenv
# initialize virtual environment
python -m venv venv
# activate virtual environment
source ./venv/Scripts/activate
# install needed packages
pip install -r requirements.txt
# done, don't forget to activate the virtual environment (second last command) when adding/removing packages
```

## Build
> The following describes the build command used for compilation on a Windows system (MSYS2).
```shell
# switch to virtual environment
source ./venv/Scripts/activate
# build
python -m nuitka \
  --mingw64 \
  --standalone \
  --warn-implicit-exceptions \
  --warn-unusual-code \
  --prefer-source-code \
  --follow-stdlib \
  --remove-output \
  --disable-bytecode-cache \
  --disable-ccache \
  --disable-dll-dependency-cache \
  --show-scons \
  --show-progress \
  --include-data-dir='./static/internals'='static/internals' \
  --python-flag='-O' \
  --enable-plugin=anti-bloat \
  --noinclude-pytest-mode=nofollow \
  --noinclude-setuptools-mode=nofollow \
  --output-dir='C:\nuitka-compile' \
  --windows-company-name='Unknown' \
  --windows-product-name='StreamerInfo' \
  --windows-product-version='1.0.0' \
  --windows-file-description='StreamerInfo serves dynamically generated illustrations containing current information about a streamers stream status (Twitch only).' \
  --windows-icon-from-ico='./static/logo.ico' \
  StreamerInfo.py
```