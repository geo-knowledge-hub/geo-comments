import React, { Component } from "react";

import { Form, Button } from "semantic-ui-react";


export class RatingTextReview extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                <Form>
                    <Form.TextArea style={{ minHeight: 130 }} />

                    <Button.Group floated="right" style={{ marginTop: "4rem" }}>
                        <Button content="Save your review" labelPosition="left" color="green" icon="save" />
                    </Button.Group>
                </Form>
            </>
        )
    }
}
