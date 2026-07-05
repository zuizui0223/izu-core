from channel_id.roi_observation_calibration import PROPOSALS


def test_roi_proposals_are_fixed():
    assert PROPOSALS == ("full_frame", "centre_65", "max_chroma_65", "max_chroma_edge_65")
