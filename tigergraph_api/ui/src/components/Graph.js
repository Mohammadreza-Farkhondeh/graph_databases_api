import React, { useState } from 'react';
import { GraphCanvas } from 'reagraph';

export function useNodes() {
    const [node, setNode] = useState({});
    return [node, setNode];
  }

export function useEdges() {
    const [edge, setEdge] = useState({});
    return [edge, setEdge];
}
  
function Graph() {
    const [nodes] = useNodes();
    const[edges] = useEdges();
    return(
    <GraphCanvas
        nodes={nodes}
        edges={edges}
    />)
};

export default Graph;