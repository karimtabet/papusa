sleep 5
if curl web:8000 | grep -q 'Home page'; then
  echo "Tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi