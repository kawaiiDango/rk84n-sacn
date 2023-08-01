## sACN receiver for Royal Kludge RK84N keyboard

I got an RK84N (sold as RK84 v2) and realized that OpenRGB doesn't support it yet.

So I made a quick and dirty sACN receiver, to make it work with Ledfx, OpenRGB and anything that suports sACN

Thanks to luke412 for decoding the RGB protocol


#### Usage

sACN/E1.31 config: 

IP: 127.0.0.84

Num pixels: 96 (16x6)

Universe: 1

Start channel: 1

FPS: Around 20 (lags at 30)


Tested on Windows 11 and Ubuntu 23.04