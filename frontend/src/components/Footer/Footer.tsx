import {FooterSection} from "./FooterStyles.ts";
import React from "react";

interface FooterProps {
    children?: React.ReactNode;
}

export default function Footer({children}: FooterProps) {
    return <FooterSection>{children}</FooterSection>;
}