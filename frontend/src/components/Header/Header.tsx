import {HeaderSection} from "./HeaderStyles.ts";
import React from "react";

interface HeaderProps {
    children?: React.ReactNode;
}

export default function Header({children}: HeaderProps) {
    return(
        <HeaderSection>
            {children}
        </HeaderSection>
    )
}