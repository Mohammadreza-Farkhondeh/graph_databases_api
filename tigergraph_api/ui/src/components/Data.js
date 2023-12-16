import React, { useState } from "react";

export function useData() {
  const [data, setData] = useState({});
  return [data, setData];
}

function Data() {
    const [data] = useData({});
    const keys = Object.keys(data);

    return (
        <table>
            <tbody>
            {keys.map((key) => (
                <tr key={key}>
                    {Object.entries(data[key]).map(([k, v]) => (
                        <td key={k}>
                            {k}: {v}
                        </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    );
}


export default Data;