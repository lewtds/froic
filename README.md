# Froic

Generate random meaningless words that comply to the English phonology and
orthography.

## Usage

```
$ python name.py --help
usage: name.py [-h] [--allow-meaningful-words] [--allow-popular-words]
               [--max-popularity INTEGER] [--max-syllables INTEGER]

optional arguments:
  -h, --help            show this help message and exit
  --allow-meaningful-words
                        Don't use the dictionary to dismiss meaningful words.
  --allow-popular-words
                        Don't use Bing to dismiss popular words.
  --max-popularity INTEGER
                        Max allowed popularity. Default is 100000.
  --max-syllables INTEGER
                        Max number of syllables. Default is 1.
```

## Origin

One day, I was reading [Hadoop: The Definitive Guide][1]. In the book, the
author quotes Hadoop's creator, Doug Cutting, saying that:

> [Hadoop is] the name my kid gave a stuffed yellow elephant.
> Short, relatively easy to spell and pronounce, meaningless, and not
> used elsewhere: those are my naming criteria. Kids are good at
> generating such. Googol is a kid’s term.

I was struck by this idea and set out to create a program to do just that:
generating names that are **short**, relatively **easy to spell and
pronounce**, **meaningless** and **not used anywhere**.

The program generated its own name.

[1]: http://shop.oreilly.com/product/0636920021773.do

## Legal

The program is released under the GNU Public License version 3. See LICENSE
for more details.

The **british-english** file comes from the **words** package version 2.1-2 in
Archlinux.
