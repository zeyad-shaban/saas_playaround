"use client";

import { useEffect, useState } from "react";

export default function IdeaGenerator() {
    const [idea, setIdea] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false)

    useEffect(() => {
        const fetchIdea = async () => {
            setLoading(true);
            try {
                const res = await fetch("/api/idea");
                const data = await res.text();
                setIdea(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchIdea();
    }, [])

    return (
        <div>
            <h1>Idea:</h1>
            <p>{loading ? "Loading..." : idea}</p>
        </div>
    )
}