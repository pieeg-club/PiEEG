# GUI
PiEEG-Club is a place, where researchers, coders, and any neuroscience enthusiast can share some scripts for PiEEG devices. Make neuroscience available for all
Please be free add your GUI in this repository  

https://pieeg.com/  
Contact: pieeg@pieeg.com  


#### Warnings
>[!WARNING]
> PiEEG  is not medical device. You are fully responsible for your personal decision to purchase this device and, ultimately, for its safe use. PiEEG is not a medical device and has not been certified by any government regulatory agency for use with the human body. Use it at your own risk.  

>[!CAUTION]
> The device must operate only from a battery - 5 V. Complete isolation from the mains power is required.! The device MUST not be connected to any kind of mains power, via USB or otherwise.   
> Power supply - only battery 5V, please read the [liability](https://pieeg.com/liability/)

git clone https://github.com/brainflow-dev/brainflow 
git checkout pieeg

python3 tools/build.py --build-periphery 
должно собраться без ошибок

cd python-package
python3 -m pip install -U .

python3 examples/tests/brainflow_get_data.py --board-id 56
