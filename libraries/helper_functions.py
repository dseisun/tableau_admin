import subprocess
import email
import settings
import smtplib
import distutils

def mkdir_if_not_exists(dir):
  if not(os.path.isdir(dir)):
    os.mkdir(dir)

def list_dict(csv_headers, csv_body):
  ret_list = []
  for line in csv_body:
    ret_list.append(
      dict(zip(csv_headers, line)))
  return ret_list

def sendEmail(email_from, email_to ,subject, body, isHTML=False):
  """Sends a simple email using internal SMTP server"""
  import email
  import smtplib
  msg = email.mime.Multipart.MIMEMultipart()
  msg['To'] = email_to
  msg['From'] = email_from
  msg['CC'] = settings.DEFAULT_CC
  msg['Subject'] = subject
  if isHTML:
    msg.attach(email.mime.Text.MIMEText(body, 'html'))
  else:
    msg.attach(email.mime.Text.MIMEText(body))
  conn = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
  conn.sendmail(email_from, email_to, msg.as_string())

def tabcmd_installed():
  if distutils.spawn.find_executable('tabcmd'):
    return True
  else:
    return False

def tableau_login(user, password, site='default'):
  if tabcmd_installed():
    if site in ['', None, 'default']:
      subprocess.call(['tabcmd', 'login',
        '-s', settings.TABLEAU_HTTP + settings.TABLEAU_HOST,
        '-u', user,
        '-p', password,
        '--no-prompt'])
    else:
      subprocess.call(['tabcmd', 'login',
        '-s', settings.TABLEAU_HTTP + settings.TABLEAU_HOST,
        '-t', site,
        '-u', user,
        '-p', password,
        '--no-prompt'])
  else:
    raise RuntimeError('tabcmd not found')

def tab_url_to_filename(url):
  return url \
  .replace(' ', '_') \
  .replace('/', '_')

def load_template(filename):
  with open(filename, "r") as f:
    template = f.read()
  return template
