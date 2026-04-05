import cv2

ip = '10.109.68.15'
user = 'Mateoramirez'
password = 'mateo1234'

urls = [
    f'rtsp://{user}:{password}@{ip}:554/stream1',
    f'rtsp://{user}:{password}@{ip}:554/stream2', 
    f'rtsp://{user}:{password}@{ip}:554/h264_stream',
    f'rtsp://{user}:{password}@{ip}:2020/stream1',
    f'rtsp://{user}:{password}@{ip}/stream1',
]

for url in urls:
    print(f'Trying {url.split("@")[1]}...')
    cap = cv2.VideoCapture(url)
    if cap.isOpened():
        print('  SUCCESS!')
        cap.release()
        break
    print('  Failed')
    cap.release()
