#!/usr/bin/python3

import hid
import sacn
import layout
import time
import queue
import threading
import platform

RK84_VID = 0x258a
RK84_PID = 0xc8
IP = "127.0.0.84"

receiver = sacn.sACNreceiver(IP)
rk84 = hid.enumerate(RK84_VID, RK84_PID)
h = hid.device()
packets_queue = queue.Queue()
packet_sender_stop_event = threading.Event()
last_packets: list[bytes] = []

@receiver.listen_on('universe', universe=1)
def sacn_callback(packet: sacn.DataPacket):
    global last_packets
    
    dmx_data = packet.dmxData
    colors = []

    for i in range(0, min(16*6*3, len(dmx_data)), 3):
        colors.append((dmx_data[i], dmx_data[i+1], dmx_data[i+2]))

    colors_dict = layout.colors_list_to_keys_dict(colors)
    packets = layout.colors_dict_to_usb_packets(colors_dict)

    # print("sending packets:")
    for packet in packets:
        packets_queue.put(packet)

    last_packets = packets

def usb_packet_sender():
    while True:
        try:
            packet = packets_queue.get(block=True, timeout=1)
            # print(packet.hex(" "))
            h.send_feature_report(packet)
        except queue.Empty:
            if packet_sender_stop_event.is_set():
                break
            else:
                # resend last packets
                for packet in last_packets:
                    h.send_feature_report(packet)

if __name__ == "__main__":
    rk_path = None
    if platform.system() == "Windows":
        for interface in rk84:
            # pprint.pprint(interface)
            if interface['usage_page'] == 65280:
                rk_path = interface['path']
                # break
    elif platform.system() == "Linux":
        if len(rk84) >=2:
            rk_path = rk84[1]['path']

    if rk_path is None:
        print("RK84N not found")
        exit(1)

    h.open_path(rk_path)
    h.set_nonblocking(1)

    packet_sender_thread = threading.Thread(target=usb_packet_sender, daemon=True)
    packet_sender_thread.start()

    receiver.start()

    print(f"sACN listening on {IP}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        receiver.stop()
        packet_sender_stop_event.set()