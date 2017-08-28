from codecs import open
from os import path
from subprocess import check_call
from tempfile import NamedTemporaryFile

from anytree import PreOrderIter


class _Render(object):

    def to_dotfile(self, filename):
        """
        Write graph to `filename`.

        >>> from anytree import Node
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)
        >>> s1a = Node("sub1A", parent=s1)
        >>> s1b = Node("sub1B", parent=s1)
        >>> s1c = Node("sub1C", parent=s1)
        >>> s1ca = Node("sub1Ca", parent=s1c)

        >>> RenderTreeGraph(root).to_dotfile("tree.dot")

        The generated file should be handed over to the `dot` tool from the
        http://www.graphviz.org/ package::

            $ dot tree.dot -T png -o tree.png
        """
        with open(filename, "w", "utf-8") as file:
            for line in self:
                file.write("%s\n" % line)

    def to_picture(self, filename):
        """
        Write graph to a temporary file and invoke `dot`.

        The output file type is automatically detected from the file suffix.

        *`graphviz` needs to be installed, before usage of this method.*
        """
        fileformat = path.splitext(filename)[1][1:]
        with NamedTemporaryFile("wb") as dotfile:
            for line in self:
                dotfile.write(("%s\n" % line).encode("utf-8"))
            dotfile.flush()
            cmd = ["dot", dotfile.name, "-T", fileformat, "-o", filename]
            check_call(cmd)


class RenderTreeGraph(_Render):

    def __init__(self, node, graph="digraph", name="tree", options=None,
                 indent=4, nodenamefunc=None, nodeattrfunc=None,
                 edgeattrfunc=None):
        """
        Dot Language Exporter.

        Args:
            node (Node): start node.

        Keyword Args:
            graph: DOT graph type.

            name: DOT graph name.

            options: list of options added to the graph.

            indent (int): number of spaces for indent.

            nodenamefunc: Function to extract node name from `node` object.
                          The function shall accept one `node` object as
                          argument and return the name of it.

            nodeattrfunc: Function to decorate a node with attributes.
                          The function shall accept one `node` object as
                          argument and return the attributes.

            edgeattrfunc: Function to decorate a edge with attributes.
                          The function shall accept two `node` objects as
                          argument. The first the node and the second the child
                          and return the attributes.

        >>> from anytree import Node
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root, edge=2)
        >>> s0b = Node("sub0B", parent=s0, foo=4, edge=109)
        >>> s0a = Node("sub0A", parent=s0, edge="")
        >>> s1 = Node("sub1", parent=root, edge="")
        >>> s1a = Node("sub1A", parent=s1, edge=7)
        >>> s1b = Node("sub1B", parent=s1, edge=8)
        >>> s1c = Node("sub1C", parent=s1, edge=22)
        >>> s1ca = Node("sub1Ca", parent=s1c, edge=42)

        >>> for line in RenderTreeGraph(root):
        ...     print(line)
        digraph tree {
            "root";
            "sub0";
            "sub0B";
            "sub0A";
            "sub1";
            "sub1A";
            "sub1B";
            "sub1C";
            "sub1Ca";
            "root" -> "sub0";
            "root" -> "sub1";
            "sub0" -> "sub0B";
            "sub0" -> "sub0A";
            "sub1" -> "sub1A";
            "sub1" -> "sub1B";
            "sub1" -> "sub1C";
            "sub1C" -> "sub1Ca";
        }

        >>> def nodenamefunc(node):
        ...     return '%s:%s' % (node.name, node.depth)
        >>> def edgeattrfunc(node, child):
        ...     return 'label="%s:%s"' % (node.name, child.name)
        >>> for line in RenderTreeGraph(root, options=["rankdir=LR;"],
        ...                             nodenamefunc=nodenamefunc,
        ...                             nodeattrfunc=lambda node: "shape=box",
        ...                             edgeattrfunc=edgeattrfunc):
        ...     print(line)
        digraph tree {
            rankdir=LR;
            "root:0" [shape=box];
            "sub0:1" [shape=box];
            "sub0B:2" [shape=box];
            "sub0A:2" [shape=box];
            "sub1:1" [shape=box];
            "sub1A:2" [shape=box];
            "sub1B:2" [shape=box];
            "sub1C:2" [shape=box];
            "sub1Ca:3" [shape=box];
            "root:0" -> "sub0:1" [label="root:sub0"];
            "root:0" -> "sub1:1" [label="root:sub1"];
            "sub0:1" -> "sub0B:2" [label="sub0:sub0B"];
            "sub0:1" -> "sub0A:2" [label="sub0:sub0A"];
            "sub1:1" -> "sub1A:2" [label="sub1:sub1A"];
            "sub1:1" -> "sub1B:2" [label="sub1:sub1B"];
            "sub1:1" -> "sub1C:2" [label="sub1:sub1C"];
            "sub1C:2" -> "sub1Ca:3" [label="sub1C:sub1Ca"];
        }
        """
        self.node = node
        self.graph = graph
        self.name = name
        self.options = options
        self.indent = indent
        self.nodenamefunc = nodenamefunc
        self.nodeattrfunc = nodeattrfunc
        self.edgeattrfunc = edgeattrfunc

    def __iter__(self):
        # prepare
        indent = " " * self.indent
        nodenamefunc = self.nodenamefunc
        if not nodenamefunc:
            def nodenamefunc(node):
                return node.name
        nodeattrfunc = self.nodeattrfunc
        if not nodeattrfunc:
            def nodeattrfunc(node):
                return None
        edgeattrfunc = self.edgeattrfunc
        if not edgeattrfunc:
            def edgeattrfunc(node, child):
                return None
        return self.__iter(indent, nodenamefunc, nodeattrfunc, edgeattrfunc)

    def __iter(self, indent, nodenamefunc, nodeattrfunc, edgeattrfunc):
        yield "{self.graph} {self.name} {{".format(self=self)
        for option in self.__iter_options(indent):
            yield option
        for node in self.__iter_nodes(indent, nodenamefunc, nodeattrfunc):
            yield node
        for edge in self.__iter_edges(indent, nodenamefunc, edgeattrfunc):
            yield edge
        yield "}"

    def __iter_options(self, indent):
        options = self.options
        if options:
            for option in options:
                yield "%s%s" % (indent, option)

    def __iter_nodes(self, indent, nodenamefunc, nodeattrfunc):
        for node in PreOrderIter(self.node):
            nodename = nodenamefunc(node)
            nodeattr = nodeattrfunc(node)
            nodeattr = " [%s]" % nodeattr if nodeattr is not None else ""
            yield '%s"%s"%s;' % (indent, nodename, nodeattr)

    def __iter_edges(self, indent, nodenamefunc, edgeattrfunc):
        for node in PreOrderIter(self.node):
            nodename = nodenamefunc(node)
            for child in node.children:
                childname = nodenamefunc(child)
                edgeattr = edgeattrfunc(node, child)
                edgeattr = " [%s]" % edgeattr if edgeattr is not None else ""
                yield '%s"%s" -> "%s"%s;' % (indent, nodename, childname,
                                             edgeattr)
