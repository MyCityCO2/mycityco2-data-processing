

# What's MyCityCO2-data-process
MyCityCO2 is an project from [Open-Net](https://open-net.ch). This project is aiming to allow citoyens to access their city carbon emission. Our importer is allowing us to create an [Odoo](https://odoo.com) database. In this project we just use [Odoo](https://odoo.com) as an calculator to our comptability, we also develop an [Odoo](https://odoo.com) module that allow company to get their carbon usage and we use this module to allow use to calculate the carbon emission. In this project we personnaly develop France importer but you can create you're own easily. In this importer we also use the [otools-rpc](https://pypi.org/project/otools-rpc/) so we can recreate the [Odoo](https://odoo.com) environment.


## How to start
Clone the repository
```bash
git clone xxx
```

then configure you're importer in the const.py file. Don't forget you're RPC url. Now you can start the program.

## Todo

- Find other ways to create chart of account that are only needed
- Check if all FrImporter function are needed in this object or the parent one.
- Add more logger.debug and check if other are needed
