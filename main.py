import pymem
import pymem.process
import time
import os
import keyboard

from pointers import *
from dearpygui import core, simple

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
clear = lambda: os.system('cls')

bChams = False
bBhop = False

def main():


    while True:
        def chams_callback(sender, data):
            global bChams
            bChams = not bChams

        def bhop_callback(sender, data):
            global bBhop
            bBhop = not bBhop

        core.set_main_window_size(400, 400)
        with simple.window("main"):
            core.add_text("Carbine CSGO")
            core.add_checkbox("Chams", callback=chams_callback)

            def main_callback(sender, data):
                if bChams == True:
                    glow_manager = pm.read_int(client + dwGlowObjectManager)

                    for i in range(1, 32):  # Entities 1-32 are reserved for players.
                        entity = pm.read_int(client + dwEntityList + i * 0x10)

                        if entity:
                            entity_team_id = pm.read_int(entity + m_iTeamNum)
                            entity_glow = pm.read_int(entity + m_iGlowIndex)

                            if entity_team_id == 2:  # Terrorist
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R 
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                            elif entity_team_id == 3:  # Counter-terrorist
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                
                if bBhop == True:
                    if keyboard.is_pressed("space"):
                        force_jump = client + dwForceJump
                        player = pm.read_int(client + dwLocalPlayer)
                        if player:
                            on_ground = pm.read_int(player + m_fFlags)
                            if on_ground and on_ground == 257:
                                pm.write_int(force_jump, 5)
                                pm.write_int(force_jump, 4)


        core.set_render_callback(main_callback)
        core.start_dearpygui(primary_window="main")


main()