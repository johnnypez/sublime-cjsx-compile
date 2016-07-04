MyComponent = React.createClass
  render: ->
    id = 1
    <a {...@props} href={"/users" + id}>
      "user id #{id}"
    </a>
