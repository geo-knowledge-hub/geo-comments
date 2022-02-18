// This file is part of GEO Feedback
// Copyright (C) 2022 GEO Secretariat.
//
// GEO Feedback is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";

import { Button, Icon } from "semantic-ui-react";

export class NewFeedbackButton extends Component {
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
    );
  }
}
