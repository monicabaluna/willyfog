# Step by step setup guide
1. Connect the board to your PC via USB.
2. Connect you board to a WiFi network.
3. Run ifconfig on your board, to find out its IP (we'll call it "board_ip").
4. Disconnect the USB cable.
5. Connect your PC to the same network.
6. From you PC, connect via ssh to the board: ssh udooer@board_ip
7. Start the server with "startwilly"
8. Now you can access the site! In your browser, type the address "board_ip:8080".
