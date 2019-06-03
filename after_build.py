
import sys
import os


"""

0、nodeppt build cassandra.md


1、删除 
<link rel=stylesheet href=//cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.min.css><link rel=stylesheet href=//cdn.staticfile.org/prism/1.15.0/themes/prism.min.css><link rel=stylesheet href=//cdn.staticfile.org/KaTeX/0.10.0-rc.1/katex.min.css>


2、替换 src=/ 为 src=


3、替换 image=/ 为 image=


4、替换 image:url('/ 为 image:url('


5、修改 css 目录下所有的 1024px 为 1300px

"""

name = 'cassandra'
if len(sys.argv) > 1:
	name = sys.argv[1]


html_content = open('dist/%s.html' % name, encoding='utf8').read()
html_content = html_content.replace('<link rel=stylesheet href=//cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.min.css><link rel=stylesheet href=//cdn.staticfile.org/prism/1.15.0/themes/prism.min.css><link rel=stylesheet href=//cdn.staticfile.org/KaTeX/0.10.0-rc.1/katex.min.css>', '')
html_content = html_content.replace('src=/', 'src=')
html_content = html_content.replace('image=/', 'image=')
html_content = html_content.replace("image:url('/", "image:url('")

open('dist/%s.html' % name, 'w', encoding='utf8').write(html_content)


for cssfile in os.listdir('dist/css'):
    csspath = os.path.join('dist', 'css', cssfile)
    css_content = open(csspath, encoding='utf8').read()
    css_content = css_content.replace('1024px', '1300px')
    open(csspath, 'w', encoding='utf8').write(css_content)

