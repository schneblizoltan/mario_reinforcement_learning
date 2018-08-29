This was created for my bachelor thesis. 

After 15 hours of learning the agent has a 55+% winrate.

The project runs just on linux. 
Special thanks to Markus Edel for the lua tcp_api. (https://github.com/zoq/gym_tcp_api)

Before you run it you have to install:
  - fceux
  - luarocks (from luarocks install lua-cjson, lua-socket)
  - python3.4 or higher
  - keras

To run:
  - start fceux
  - load "super_mario_bros.lua" from mario_rom_scripts
  - open "super-mario.nes" from mario_rom
  - set up rf_client and run it
  - the agent will start to learn
