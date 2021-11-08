
import React, { Component } from "react";

import { Grid } from "semantic-ui-react";

import { RatingModal } from "./RatingModal";
import { NewReviewButton } from "./button/NewReviewButton";
import { AllFeedbackButton } from "./button/AllFeedbackButton";
import { ListRatingModal } from "./ListRatingModal";


export class RatingApp extends Component {
    constructor(props) {
        super(props);

        this.state = { isFeedbackModalOpen: false, isNewReviewModalOpen: false };
    }

    modalFeedbackHandler = () => {
        this.setState((prevState) => {
            return {
                ...prevState,
                isFeedbackModalOpen: !prevState.isFeedbackModalOpen
            }
        })
    }

    modalNewReviewHandler = () => {
        this.setState((prevState) => {
            return {
                ...prevState,
                isNewReviewModalOpen: !prevState.isNewReviewModalOpen
            }
        })
    }

    render() {
        return (
            <>
                <Grid>
                    <Grid.Row columns={2}>
                        <Grid.Column>
                            <AllFeedbackButton modalHandler={this.modalFeedbackHandler} />
                        </Grid.Column>
                        <Grid.Column>
                            <NewReviewButton modalHandler={this.modalNewReviewHandler} />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <RatingModal
                    modalHandler={this.modalNewReviewHandler}
                    isModalOpen={this.state.isNewReviewModalOpen}
                />

                <ListRatingModal
                    modalHandler={this.modalFeedbackHandler}
                    isModalOpen={this.state.isFeedbackModalOpen}
                />
            </>
        )
    }
}
