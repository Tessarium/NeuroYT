import React, { Component } from "react"


class Header extends Component {
    render() {
        const {title, subtitle} = this.props;

        const styles = {
            header: {
                width: '100%',
                paddingBottom: '5%',
                textAlign: 'center',
                paddingLeft: '30%',
                paddingRight: '30%',
            },

            title: {
                fontSize: 40,
                lineHeight: '34px',
            },

            subtitle: {
                fontSize: 24,
                lineHeight: '26px',
            },
        };

        return (
            <div style={styles.header}>
                <h1 style={styles.title}>{title}</h1>
                {subtitle && (
                    <h2 style={styles.subtitle}>{subtitle}</h2>
                )}
            </div>
        )
    }
}
export default Header;