sleep 30
if curl localhost:8000 | grep -q 'Welcome to your new Wagtail site!'; then
  echo "Tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi
