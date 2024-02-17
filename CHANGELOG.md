# CHANGELOG



## v0.3.0 (2024-02-17)

### Feature

* feat: prevent multiple useage of modbus client ([`189cba7`](https://github.com/The-Smartest-Home/hass_inspirair/commit/189cba76be2eedee6f28488cd9d044d3a6006dbe))

### Fix

* fix: remove duplicate connect ([`48204d6`](https://github.com/The-Smartest-Home/hass_inspirair/commit/48204d6158e9b991ea1bdad9edeee5f81cd653c1))

* fix: use sync reconnect ([`4c7a606`](https://github.com/The-Smartest-Home/hass_inspirair/commit/4c7a606a1a38721e21a49fb0b755c3377c8779c5))

### Refactor

* refactor: use new modbus clients for every request ([`a8868d2`](https://github.com/The-Smartest-Home/hass_inspirair/commit/a8868d201af0b43480e333a302ce5969956fed96))

### Unknown

* Create dependabot.yml ([`19d6d64`](https://github.com/The-Smartest-Home/hass_inspirair/commit/19d6d64bfa27cb0b69c63e481b4aa159495e1dcc))


## v0.2.0 (2024-02-11)

### Feature

* feat: improve serial reconnection behavior ([`12e6572`](https://github.com/The-Smartest-Home/hass_inspirair/commit/12e657251238545e2f6334a1dce5e5e0d95b934d))


## v0.1.1 (2024-02-11)

### Fix

* fix: use rtu framer for default serial client ([`f1063e0`](https://github.com/The-Smartest-Home/hass_inspirair/commit/f1063e050926171380a3adf226464366784d3323))

### Refactor

* refactor: make logging configurable ([`f8f2c23`](https://github.com/The-Smartest-Home/hass_inspirair/commit/f8f2c23b6e3241a9bfc6405050141288713ff5fc))


## v0.1.0 (2024-02-11)

### Feature

* feat: fix sensor types ([`d840166`](https://github.com/The-Smartest-Home/hass_inspirair/commit/d840166864ca916f19cb703f691ccaa396e5744e))

* feat: add workflows ([`6130d6d`](https://github.com/The-Smartest-Home/hass_inspirair/commit/6130d6db1faa2ce560859591fbdbb29872bc630a))

* feat: add mqtt auth ([`3d7c66b`](https://github.com/The-Smartest-Home/hass_inspirair/commit/3d7c66bfee9a610209c001e28da5404fafc10b9e))

* feat: add object id to config ([`ec29077`](https://github.com/The-Smartest-Home/hass_inspirair/commit/ec2907766aa9bfbac9658b028faf1953a9d643ce))

* feat: add proper device classes ([`6c5c0e5`](https://github.com/The-Smartest-Home/hass_inspirair/commit/6c5c0e5495d6d03add14649550ff014e554e8cec))

* feat: collect all environment variables ([`38a94c9`](https://github.com/The-Smartest-Home/hass_inspirair/commit/38a94c9e7c2a9d462c8525eebdd1aac4c08fd20c))

* feat: reuse connections in loop ([`92f8ff0`](https://github.com/The-Smartest-Home/hass_inspirair/commit/92f8ff021a0d99ac8e27843d4abaa9b39184f984))

* feat: bootstrap home assistant registration and callback ([`8607e33`](https://github.com/The-Smartest-Home/hass_inspirair/commit/8607e337a6dfff9d981303face088807d8683832))

* feat: add main loop ([`78676a1`](https://github.com/The-Smartest-Home/hass_inspirair/commit/78676a10dd49b7dd66c0d489623638f81758d289))

* feat: add modbus read error handling ([`a413956`](https://github.com/The-Smartest-Home/hass_inspirair/commit/a4139563ef64518ca43166f1f7bd24437f4ed575))

* feat: add modbus test env ([`93575b5`](https://github.com/The-Smartest-Home/hass_inspirair/commit/93575b5b75dc9cc7ac1d698bccdfd5afca826a02))

* feat: add translations for attributes ([`2401e22`](https://github.com/The-Smartest-Home/hass_inspirair/commit/2401e2274eb3e23d39c80bdee91bbe6819cf3c95))

* feat: map modbus data on ha data ([`80a0ff9`](https://github.com/The-Smartest-Home/hass_inspirair/commit/80a0ff930d34b129bb76d21b0532b0185ad58f3e))

* feat: add ha sensor mappings ([`cf44018`](https://github.com/The-Smartest-Home/hass_inspirair/commit/cf44018b52540f5c3e5d4e9028920f7599e43f94))

* feat: add modbus client ([`c326423`](https://github.com/The-Smartest-Home/hass_inspirair/commit/c326423a44e47bb9dca031f0ef2359d4f1fa5cbc))

* feat: bootstrap i18n ([`f7f39f6`](https://github.com/The-Smartest-Home/hass_inspirair/commit/f7f39f6a73e2fe78af97082cd91385e79a2d5514))

* feat: init project ([`5df12fc`](https://github.com/The-Smartest-Home/hass_inspirair/commit/5df12fcf091124a4b0e923312fd9845a45e4f47b))

### Refactor

* refactor: rename package ([`aed77d6`](https://github.com/The-Smartest-Home/hass_inspirair/commit/aed77d68ff4d00150a9bdc464f91eeba3e48427b))

* refactor: handle modbus error ([`5b1aff3`](https://github.com/The-Smartest-Home/hass_inspirair/commit/5b1aff348a69e280cface83811f791d5d69ea7aa))

* refactor: read config from env ([`b5e0857`](https://github.com/The-Smartest-Home/hass_inspirair/commit/b5e0857af16e7f9323c44a275bbeaf3cf1490de6))

### Unknown

* Initial commit ([`4340db9`](https://github.com/The-Smartest-Home/hass_inspirair/commit/4340db9ae88ca423d85677e538355c0f35a6111d))
