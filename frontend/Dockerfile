FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  libx11-xcb1 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-randr0 \
  libxcb-render-util0 \
  libxcb-shape0 \
  libxcb-xkb1 \
  libxkbcommon-x11-0 \
  libxcb-cursor0 \
  libqt6gui6 \
  libqt6widgets6 \
  libqt6core6 \
  x11-utils \
  --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=:0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN ls 

COPY client.py .
COPY interface.py .

RUN chmod +x interface.py

CMD ["python", "interface.py"] 