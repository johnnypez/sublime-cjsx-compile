# Sublime Text 2/3 - CJSX Compile

Forked from https://github.com/surjikal/sublime-coffee-compile to provide a cjsx compiler

## Requirements

```bash
npm install -g coffee-react-transform
```

## Installation

```
Package Control > Add Repository
enter: https://github.com/johnnypez/sublime-cjsx-compile

Package Control > Install Package
select: sublime-cjsx-compile
```

Get your path to `cjsx-transform`

```
which cjsx-transform
> /Users/ronburgundy/.nvm/v0.10.40/bin
```

Add that to your plugin settings in `Sublime Text > Preferences > Package Settings > CJSX Compile > Settings - User`

e.g.

```json
{
  "cjsx_transform_path": "/Users/ronburgundy/.nvm/v0.10.40/bin"
}
```
