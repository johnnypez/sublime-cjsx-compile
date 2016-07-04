import os
try:                import JSON
except ImportError: import json as JSON

try:
    from .execute import execute
    from .exceptions import CoffeeCompilationUnknownError, CoffeeCompilationOSError, CoffeeModuleNotFoundError, CoffeeExecutableNotFoundError
except ValueError:
    from execute import execute
    from exceptions import CoffeeCompilationUnknownError, CoffeeCompilationOSError, CoffeeModuleNotFoundError, CoffeeExecutableNotFoundError


class CoffeeCompiler(object):

    def __init__(self, node_path=None):
        self.node_path = node_path

    def compile(self, coffeescript, options={}):
        raise NotImplementedError()

    def _execute(self, args, coffeescript='', cwd=None):
        path = self._get_path()
        self.path = path # FIXME: Side effect... required by exceptions raised from derived classes.
        try:
            javascript, error = execute(args=args, message=coffeescript, path=path, cwd=cwd)
            if error: raise CoffeeCompilationUnknownError(path, error)
            return javascript
        except OSError as e:
            raise CoffeeCompilationOSError(self.path, e)

    def _get_path(self):
        path = os.environ.get('PATH', '').split(os.pathsep)
        if self.node_path: path.insert(0, self.node_path)
        return path


class CoffeeCompilerModule(CoffeeCompiler):

    def __init__(self, node_path=None, cwd=None):
        CoffeeCompiler.__init__(self, node_path)
        self.cwd = cwd

    def compile(self, coffeescript, options={}):
        bootstrap  = self._get_bootstrap_script(options)
        javascript = self._execute(
            args=['node', '-e', bootstrap]
          , coffeescript=coffeescript
          , cwd=self.cwd
        )
        if javascript.startswith('module.js'):
            require_search_paths = self._get_require_search_paths()
            raise CoffeeModuleNotFoundError(self.path, javascript, require_search_paths)
        return javascript

    def _get_bootstrap_script(self, options={}):
        return """
        console.log(require.paths);
        var coffee = require('coffee-script');
        var cjsx_transform = require('coffee-react-transform');
        function transform(code){
          return coffee.compile(cjsx_transform(code), {bare: true});
        }
        var buffer = "";
        process.stdin.on('data', function(d) { buffer += d; });
        process.stdin.on('end',  function()  { console.log(transform(buffer)); });
        process.stdin.read();
        """

    def _get_require_search_paths(self):
        return self._execute(
            args=['node', '-e', "console.log(require.paths)"]
          , cwd=self.cwd
        )

    def _options_to_json(self, options={}):
        return 'null'
        return JSON.dumps({
            'bare': options.get('bare', False)
          , 'literate': options.get('literate', False)
        })


class CoffeeCompilerExecutable(CoffeeCompiler):

    def __init__(self, node_path=None, cjsx_transform_path=None, cjsx_transform_executable=None):
        CoffeeCompiler.__init__(self, node_path)
        self.cjsx_transform_path       = cjsx_transform_path
        self.cjsx_transform_executable = cjsx_transform_executable

    def compile(self, coffeescript, args):
        javascript = self._execute(
            coffeescript=coffeescript
          , args=([self.cjsx_transform_executable] + args)
        )
        if javascript == "env: node: No such file or directory":
            raise CoffeeExecutableNotFoundError(self.path, javascript)
        return javascript

    def _get_path(self):
        path = CoffeeCompiler._get_path(self)
        if self.cjsx_transform_path: path.insert(0, self.cjsx_transform_path)
        return path


class CoffeeCompilerExecutableVanilla(CoffeeCompilerExecutable):

    def compile(self, coffeescript, options):
        return CoffeeCompilerExecutable.compile(self,
            coffeescript=coffeescript
          , args=[]
        )

    def _options_to_args(self, options):
        # args = ['--stdio', '--print']
        # if options.get('bare'): args.append('--bare')
        # if options.get('literate'): args.append('--literate')
        return []
