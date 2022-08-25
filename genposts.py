#!/usr/bin/env python3

#
# ToDo:
# 1) Move postlist generation code to layout (maybe fix "blog" from bulma-clean)
# 2) Figure out how to get Jekyll to process Markdown for pagination templates
# 3) Figure out how to filter on both collections and tags
# 4) Figure out how categories work and add by-category paginated groups
# 5) Figure out what happens if there is no "master" permalink (create one index for "all posts")
#

import datetime, os

def createTemplate(path, collection = None, category = None, tag = None, sub = None, sort = None):
	os.makedirs(os.path.dirname(path), exist_ok = True)

	if category:
		targ = category
	elif collection or tag:
		targ = '-'.join([value for value in [collection, tag] if value is not None])
	else:
		targ = 'blog' # dummy default (not currently tested or used)

	target = f'{targ}-{sub}' if sub else f'{targ}'

	with open(path, 'w') as fp:
		fp.write('---\n')
		fp.write('layout: blog\n')
		fp.write('pagination:\n')
		fp.write('  enabled: true\n')

		# This example only supports one collection/category/tag per post for now

		if collection:
			fp.write('  collection: {0}\n'.format(collection))

		if category:
			fp.write('  category: {0}\n'.format(category))

		if tag:
			fp.write('  tag: {0}\n'.format(tag))

		if sort:
			tokens = sort.split('/')

			fp.write('  sort_field: {0}\n'.format(tokens[0]))

			if len(tokens) > 1 and tokens[1] == 'rev':
				fp.write('  sort_reverse: true\n')
			else:
				fp.write('  sort_reverse: false\n')

		fp.write('  per_page: 10\n')
		fp.write('  permalink: /page:num.html\n')
		fp.write('permalink: /{0}/\n'.format(target))
		fp.write('---\n')
		fp.write('\n')

		fp.write('### Settings:\n')
		fp.write('\n')

		fp.write('| Setting    | Value |\n'.format(collection))
		fp.write('| ---------- | ----- |\n'.format(collection))
		fp.write('| Collection |  {0}  |\n'.format(collection))
		fp.write('| Tag        |  {0}  |\n'.format(tag))
		fp.write('| Sorting    |  {0}  |\n'.format(sort))
		fp.write('\n')

	return f'[{target}](/{target}/) (sorted by {sort})' # return link to template index page in MD format

aTags = ['TagA1', 'TagA2', 'TagA3', 'TagA4', None]
bTags = ['TagB1', 'TagB2', None]

aIndx = 0
bIndx = 0

today = datetime.date.today()

for srcdir in ['_category1', '_category2', '_category3', '_pages', '_posts']:
	os.makedirs(os.path.join(os.getcwd(), srcdir), exist_ok = True)

	for fileno in range(93):
		name = f'{srcdir[1:]}-post-number-{fileno + 1}'

		date = today + datetime.timedelta(days = fileno)

		if srcdir in ['_posts']:
			path = os.path.join(os.getcwd(), srcdir, f'{date}-{name}.md')
		else:
			path = os.path.join(os.getcwd(), srcdir, f'{name}.md')

		tags = [tag for tag in [aTags[aIndx], bTags[bIndx]] if tag is not None]

		aIndx = (aIndx + 1) % len(aTags)
		bIndx = (bIndx + 1) % len(bTags)

		with open(path, 'w') as fp:
			escPath = path.replace("_", "\\_")

			fp.write('---\n')

			if srcdir in ['_posts']:
				fp.write('layout: post\n')
			else:
				fp.write('layout: page\n')

			fp.write(f'title: {name}\n')

			if srcdir not in ['_posts']:
				fp.write(f'date: {date}\n')

			if ((fileno + 1) % 3) == 0:
				fp.write(f'category: DivisibleByThree\n')

			if tags:
				fp.write(f'tags: {" ".join(tags)}\n')

			fp.write('---\n')

			fp.write('File Information:\n')

			fp.write(f'* Path: {escPath}\n')
			fp.write(f'* Coln: {srcdir[1:]}\n')
			fp.write(f'* Tags: {" ".join(tags) if tags else "None"}\n')

#
# Generage category templates (all reside in _lists source directory)
#

targdir = os.path.join(os.getcwd(), '_lists')

templates = [ ]

for srcdir in ['_category1', '_category2', '_category3', '_posts']:
	name = srcdir[1:] # remove underscore for use as permalink

	sort = 'date/rev' if srcdir in ['_posts'] else 'title'

	templates.append(createTemplate(os.path.join(targdir, f'{name}-list.md'),   collection = name,                 sort =  sort))
	templates.append(createTemplate(os.path.join(targdir, f'{name}-bydate.md'), collection = name, sub = 'bydate', sort = 'date'))
	templates.append(createTemplate(os.path.join(targdir, f'{name}-byname.md'), collection = name, sub = 'byname', sort = 'title'))

for tag in [tag for tag in aTags + bTags if tag is not None]:
	templates.append(createTemplate(os.path.join(targdir, f'{tag}-list.md'),   tag = tag,                 sort = 'date/rev'))
	templates.append(createTemplate(os.path.join(targdir, f'{tag}-bydate.md'), tag = tag, sub = 'bydate', sort = 'date'))
	templates.append(createTemplate(os.path.join(targdir, f'{tag}-byname.md'), tag = tag, sub = 'byname', sort = 'title'))

for category in ['DivisibleByThree']:
	templates.append(createTemplate(os.path.join(targdir, f'DivisibleByThree.md'), category = category, sort = 'date/rev'))

#
# Generate landing page
#

with open(os.path.join(os.getcwd(), 'index.md'), 'w') as fp:
	fp.write('---\n')
	fp.write('layout: page\n')
	fp.write('---\n')

	fp.write('# Pagination Test\n')

	fp.write('\n')
	fp.write('### Paginated Posts:\n')

	for template in templates:
		fp.write(f'* {template}\n')

	fp.write('\n')
	fp.write('### Regular Pages:\n')

	for fileno in range(93):
		fp.write(f'* [pages-post-number-{fileno + 1}](/pages-post-number-{fileno + 1}/)\n')

#
# Create static pages: "blog" layout and _config.yml
#

os.makedirs(os.path.join(os.getcwd(), '_layouts'), exist_ok = True)

with open(os.path.join(os.getcwd(), '_layouts', 'blog.html'), 'w') as fp:
	fp.write('---\n')
	fp.write('layout: page\n')
	fp.write('---\n')
	fp.write('\n')

	fp.write('{{ content | markdownify }}\n')
	fp.write('\n')

	fp.write('<h3>Paginated Posts:</h3>\n')
	fp.write('<ul>\n')
	fp.write('{% for post in paginator.posts %}\n')
	fp.write('  <li><a href="{{ post.url }}">{{ post.title }}</a></li>\n')
	fp.write('{% endfor %}\n')
	fp.write('</ul>\n')
	fp.write('{% if paginator.total_pages > 1 %}\n')
	fp.write('<ul>\n')
	fp.write('  {% if paginator.previous_page %}\n')
	fp.write('  <li>\n')
	fp.write('    <a href="{{ paginator.previous_page_path | prepend: site.baseurl }}">Previous</a>\n')
	fp.write('  </li>\n')
	fp.write('  {% endif %}\n')
	fp.write('  {% if paginator.next_page %}\n')
	fp.write('  <li>\n')
	fp.write('    <a href="{{ paginator.next_page_path | prepend: site.baseurl }}">Next</a>\n')
	fp.write('  </li>\n')
	fp.write('  {% endif %}\n')
	fp.write('</ul>\n')
	fp.write('{% endif %}\n')

with open(os.path.join(os.getcwd(), '_config.yml'), 'w') as fp:
	fp.write('title: Dummy Pagination Test\n')
	fp.write('\n')
	fp.write('url: "https://larabell.org"\n')
	fp.write('baseurl: ""\n')
	fp.write('\n')
	fp.write('collections:\n')
	fp.write('  pages:\n')
	fp.write('    output: true\n')
	fp.write('    permalink: /:name/\n')
	fp.write('  posts:\n')
	fp.write('    output: true\n')
	fp.write('    permalink: /blog/:year/:month/:day/:title:output_ext\n')
	fp.write('\n')
	fp.write('show_excerpts: true\n')
	fp.write('\n')
	fp.write('date_format: "%-d %b %Y"\n')
	fp.write('\n')
	fp.write('future: true\n')
	fp.write('\n')
	fp.write('plugins:\n')
	fp.write('  - jekyll-feed\n')
	fp.write('  - jekyll-paginate-v2\n')
	fp.write('  - jekyll-themes-control\n')
	fp.write('\n')
	fp.write('theme: bulma-clean-theme\n')
	fp.write('\n')
	fp.write('collections:\n')
	fp.write('  category1:\n')
	fp.write('    output: true\n')
	fp.write('    indexpage: /category1/index\n')
	fp.write('    permalink: /category1/:title:output_ext\n')
	fp.write('  category2:\n')
	fp.write('    output: true\n')
	fp.write('    permalink: /category2/:title:output_ext\n')
	fp.write('  category3:\n')
	fp.write('    output: true\n')
	fp.write('    permalink: /category3/:title:output_ext\n')
	fp.write('  pages:\n')
	fp.write('    output: true\n')
	fp.write('    permalink: /:name/\n')
	fp.write('\n')
	fp.write('pagination:\n')
	fp.write('  enabled: true\n')
	fp.write('\n')
	fp.write('include:\n')
	fp.write('  - _lists\n')
	fp.write('\n')
	fp.write('exclude:\n')
	fp.write('  - genposts.py\n')
	fp.write('  - Makefile\n')
