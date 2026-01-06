#!/bin/zsh

echo "Starting load generation: 500 requests..."

for i in {1..500}
do
  # Generate random values for key features
  AGE=$(( ( RANDOM % 50 ) + 30 ))      # Age between 30-80
  CHOL=$(( ( RANDOM % 150 ) + 180 ))   # Cholesterol between 180-330
  THAL=$(( ( RANDOM % 100 ) + 100 ))   # Max Heart Rate between 100-200
  CP=$(( RANDOM % 4 ))                 # Chest pain type 0-3

  curl -s -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d "{
      \"age\": $AGE,
      \"sex\": 1,
      \"cp\": $CP,
      \"trestbps\": 145,
      \"chol\": $CHOL,
      \"fbs\": 1,
      \"restecg\": 0,
      \"thalach\": $THAL,
      \"exang\": 0,
      \"oldpeak\": 2.3,
      \"slope\": 0,
      \"ca\": 0,
      \"thal\": 1
    }" > /dev/null

  # Optional: progress indicator every 50 requests
  if (( $i % 50 == 0 )); then
    # Formula: min + (RANDOM % (max - min + 1))
    sleep $(( 5 + RANDOM % 6 ))
    echo "Sent $i requests..."
  fi
done

echo "Done. Check Prometheus/Grafana."