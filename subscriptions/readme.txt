This is a full framework for emailing reports to users. Some of the features:
	- Email multiple users
	- Each email may contain multiple dashboards from multiple different workbooks
	- (Slightly) intelligent caching. If a report is going to many users, it only pulls it down once.
	- Filtered subscriptions. This solves for: User A is only supposed to see data for California, and User B data for Wisconsin
	- Dynamic Filters (Sort of). Ex: Report can always be filtered to show only last saturday's data.

### What each file does:

	### TableauSubscription.py:

	This holds the meat of the logic. This is what you'll run via cron or windows task scheduler. More on this below under "How to create a subscription". This file can take a lot of parameters when being run for debugging purposes, but generally it will just need the path to a config file

	### Subscription.py

	This holds 2 classes. Subscription, which contains some helper methods. Each subscription will also contain a list of SubscriptionRows. You will feed this a csv that gives all the email/dashboard combinations, and these will all be represented as a SubscriptionRow

	### TabEmail

	This is a module for sending out emails. It currently is hard set to email out png's for the dashboard, and can allow for a static pdf attachment (Frequently used for readme's). The reason we hard coded down to png is that if you want to embed an image in your email, it must be a png. Read: https://sendgrid.com/blog/embedding-images-emails-facts/ (CID embedded Images) for more information on how to achieve this. The boiler plate is there, you just need to reference the image from your email body.

	### ListParamSub.py

	This file reads in your list of email/dashboards and dynamically swaps out certain parameters it finds. This was build for dynamic date reporting, although in theory it could be extended to do much more.

	### test_subscription/List.csv

	This is a combination of all the email/dashboards you'd like to have emailed out. It automatically puts all dashboards with the same email address into the same email. 

	It expects a header of: Email, URL, <Param1>, <Value1>
	The <Param1>, <Value1> is for URL filtering. Param is the name of the field, and Value is the value you'd like to filter for the field. This supports any number of parameters. To add more, just add a <Param2>, <Value2> to the header. This is also where you would set your dynamic filters. Look at the sample to get an idea of how it could be used.

	### test_subscription/config.xml

	This contains information that is specific to the subscription. Where to save/archive files, and email text.

### How to create a subscription

	1) Create a folder for your new subscription. Look at 'test_subscription' as a template. It doesn't necessarily need to be in the same dir as the subscription code
	2) Update List.csv and config.xml to your particular subscription settings
	3) Run 'python TableauSubscription.py --config <path to your config file>'
		- If you'd like to temporarily override who the emails go to (so you don't spam your users when debugging), use the --to_override parameter.
		- If you have a long list for the subscription, but for debugging only want to use the first 'X' rows of the list, use the --take_top parameter
	4) Once you have a working execution schedule it as you'd like with cron or windows task scheduler. Remember, cron and windows task scheduler don't have access to your PATH, so your command will likely be something like '/usr/bin/python TableauSubscription.py ...'