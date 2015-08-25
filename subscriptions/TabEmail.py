import email
import os
def TabEmail(email_to, email_from, email_subject, email_body, email_attachments_png=[], email_attachment_pdf=''):
	
	msg = email.mime.Multipart.MIMEMultipart()
	msg['From'] = email_from
	msg['Subject'] = email_subject
	msg.attach(email.mime.Text.MIMEText(email_body, 'html'))

	for i,attachement in enumerate(email_attachments_png):
		print attachement
		attach_img = email.MIMEImage.MIMEImage(open(attachement, 'rb').read())
		attach_img.set_param('name', os.path.split(attachement)[1])
		attach_img.add_header('Content-ID', '<png_img{0}>'.format(i))
		msg.attach(attach_img)

	if email_attachment_pdf:
		email_static_attach = email.MIMEBase.MIMEBase('application', 'pdf')
		email_static_attach.set_payload(open(email_attachment_pdf, 'rb').read())
		email.encoders.encode_base64(email_static_attach)
		email_static_attach.set_param('name', os.path.split(email_attachment_pdf)[1])
		msg.attach(email_static_attach)
	return msg