# InfraSnow Downloader

This tool is meant to replace the existing data download steps for the [FPGA Company](https://snow-sen.com/) [InfraSnow](https://snow-sen.com/infrasnow-ssa-sensor-2/) instrument. The tool can download the onboard measurement data from the InfraSnow instrument via USB connection to a host computer.

## User Requirements

> [!CAUTION]
> If you are on Windows, you must ensure that your USB device drivers are up-to-date. Most Windows 10 and Windows 11 machines will auto-download the correct drivers but if you are using a managed PC, you may need to get assistance from your IT staff to install a compatible `STMicroelectronics Virtual COM Port` driver.

Download the prebuilt executable for your platform from the [Releases page](https://github.com/m9brady/infrasnow-download/releases) and follow the [user guide](documentation/README.md). Consult the next sections if you want to run the Python code yourself or build your own executable.

## Development

### Environment Creation

Create a new Python3 venv or mamba environment (mamba seems to work better) and add packages from `requirements.txt`. If you also want to build executables you need to install `pyinstaller`. 

Once `pyserial` is installed, you can choose to run `infrasnow_downloader.py` manually or proceed to build an executable.

### Building the Executable

Using `pyinstaller`:

```shell
pyinstaller --console --onefile --icon assets/infrasnow.ico infrasnow_downloader.py
```

This will create `build` and `dist` directories. The executable will be under the `dist` directory.

Explanation of build options:
- `--console`: open a new console when the executable is double-clicked by the user
- `--onefile`: rather than the default of a "one-folder" bundle, create a "one-file" bundled executable
- `--icon <icon-path>`: add an icon to the executable just for fun
