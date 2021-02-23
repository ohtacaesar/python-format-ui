from string import Formatter

from flask import Flask, render_template, request

app = Flask(__name__)

last_args = {}


@app.route('/', methods=['get', 'post'])
def home():
  template = request.form.get('template', '')

  input_args = {}
  input_args.update(last_args)
  app.logger.info(input_args)
  for k, v in request.form.to_dict().items():
    if k.startswith("args.") and v:
      input_args[k[5:]] = v

  args = dict()
  error = None
  try:
    result = Formatter().parse(template)
    for tup in result:
      field = tup[1]
      if field:
        args[field] = input_args.get(field)
  except Exception as e:
    app.logger.error(e)
    error = str(e)

  output = ""
  try:
    output = template.format(**input_args)
    last_args.update(args)
  except Exception as e:
    app.logger.error(e)

  return render_template(
    "home.html",
    template=template,
    args=args,
    output=output,
    error=error,
  )


if __name__ == '__main__':
  app.run(host="0.0.0.0")
