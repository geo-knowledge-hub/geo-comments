// This file is part of GEO Feedback
// Copyright (C) 2022 GEO Secretariat.
//
// GEO Feedback is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";

import { Container, Grid } from "semantic-ui-react";

import { FeedbackModal } from "./components/FeedbackModal";

import { NewFeedbackButton } from "./components/button/NewFeedbackButton";
import { ListFeedbackButton } from "./components/button/ListFeedbackButton";

export class UserFeedbackApp extends Component {
  constructor(props) {
    super(props);

    this.state = { isFeedbackModalOpen: false, isNewFeedbackModalOpen: false };
  }

  modalFeedbackHandler = () => {
    this.setState((prevState) => {
      return {
        ...prevState,
        isFeedbackModalOpen: !prevState.isFeedbackModalOpen,
      };
    });
  };

  modalNewReviewHandler = () => {
    this.setState((prevState) => {
      return {
        ...prevState,
        isNewFeedbackModalOpen: !prevState.isNewFeedbackModalOpen,
      };
    });
  };

  render() {
    return (
      <Container>
          <Grid>
            <Grid.Row columns={2}>
              <Grid.Column>
                <ListFeedbackButton modalHandler={this.modalFeedbackHandler} />
              </Grid.Column>
              <Grid.Column>
                <NewFeedbackButton modalHandler={this.modalNewReviewHandler} />
              </Grid.Column>
            </Grid.Row>
          </Grid>

          <FeedbackModal
            modalHandler={this.modalNewReviewHandler}
            isModalOpen={this.state.isNewFeedbackModalOpen}
          />

          {/* ToDo: This will be implemented in a near future */}
          {/* <ListRatingModal
          modalHandler={this.modalFeedbackHandler}
          isModalOpen={this.state.isFeedbackModalOpen}
        /> */}
      </Container>
    );
  }
}
