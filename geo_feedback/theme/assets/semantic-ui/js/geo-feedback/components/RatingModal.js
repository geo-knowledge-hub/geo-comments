

import React, { Component } from "react";

import { RatingFiveStars } from "./RatingFiveStars";
import { RatingTextReview } from "./RatingTextReview";
import { Modal, Grid, Container, Label } from "semantic-ui-react";


export class RatingModal extends Component {
    constructor(props) {
        super(props);
    }


    render() {

        const categories = ["Completeness", "Discoverability", "Readability", "Data quality", "Service quality"];

        return (

            <Modal
                closeIcon
                size={"large"}
                centered={false}
                dimmer={"blurring"}
                open={this.props.isModalOpen}
                onClose={this.props.modalHandler}
            >
                <Modal.Header>Add your review</Modal.Header>
                <Modal.Content>
                    <Grid columns={2} divided padded>
                        <Grid.Column width={5}>
                            <Container style={{ marginBottom: "2rem" }}>
                                <Label circular color={"blue"} key={"blue"}>
                                    1
                                </Label>
                                {" "}
                                Share your experience with this resource.
                            </Container>

                            <RatingFiveStars
                                categories={categories}
                            />
                        </Grid.Column>

                        <Grid.Column centered width={11}>

                            <Container style={{ marginBottom: "2rem" }}>
                                <Label circular color={"blue"} key={"blue"}>
                                    2
                                </Label>
                                {" "}
                                Tell the community a bit about your experiences with this resource.
                            </Container>
                            <RatingTextReview />
                        </Grid.Column>
                    </Grid>
                </Modal.Content>
            </Modal>
        )
    }
}
