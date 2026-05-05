"use client";

import { useState } from "react";

export default function TimerButton() {
    const [count, setCount] = useState(0);

    const onButtonClick = () => {
        setCount(count + 1);
    }

    return (
        <div>
            <button onClick={onButtonClick}>Click Me!</button>
            <p>{count}</p>
        </div>
    )
}