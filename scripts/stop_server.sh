#!/bin/bash

# 실행중인 FastAPI 앱의 PID를 배열로 저장
PIDS=($(ps aux | grep uvicorn | grep -v grep | awk '{print $2}'))

if [ ${#PIDS[@]} -eq 0 ]; then
  echo "FastAPI 앱이 실행중이지 않습니다."
else
  echo "FastAPI 앱을 종료합니다."

  # 모든 PID에 대해서 순회하며 각각 종료
  for PID in "${PIDS[@]}"; do
    echo "PID: $PID 종료"
    kill $PID
  done
fi

echo "FastAPI 앱 종료 완료"
