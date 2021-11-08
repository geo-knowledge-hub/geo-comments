import React, { Component } from "react";

import { Button, Icon } from "semantic-ui-react";


export class NewReviewButton extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <>
                <Button
                    basic
                    compact
                    size="medium"
                    color="gray"
                    onClick={this.props.modalHandler}
                >
                    <Icon name="conversation" /> Add your review
                </Button>
            </>
        )
    }
}
