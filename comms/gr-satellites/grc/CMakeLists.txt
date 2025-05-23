# Copyright 2011 Free Software Foundation, Inc.
#
# This file was generated by gr_modtool, a tool from the GNU Radio framework
# This file is a part of gr-satellites
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

install(FILES
    satellites_aausat4_remove_fsm.block.yml
    satellites_adsb_kml.block.yml
    satellites_append_crc32c.block.yml
    satellites_ax100_decode.block.yml
    satellites_beesat_classifier.block.yml
    satellites_bme_submitter.block.yml
    satellites_bme_ws_submitter.block.yml
    satellites_cc11xx_packet_crop.block.yml
    satellites_check_address.block.yml
    satellites_check_ao40_uncoded_crc.block.yml
    satellites_check_astrocast_crc.block.yml
    satellites_check_cc11xx_crc.block.yml
    satellites_check_crc16_ccitt.block.yml
    satellites_check_crc16_ccitt_false.block.yml
    satellites_check_crc.block.yml
    satellites_check_eseo_crc.block.yml
    satellites_check_swiatowid_crc.block.yml
    satellites_check_tt64_crc.block.yml
    satellites_convolutional_encoder.block.yml
    satellites_costas_loop_8apsk_cc.block.yml
    satellites_crc_append.block.yml
    satellites_crc_check.block.yml
    satellites_decode_ra_code.block.yml
    satellites_decode_rs.block.yml
    satellites_decode_rs_ccsds.block.yml
    satellites_descrambler308.block.yml
    satellites_distributed_syncframe_soft.block.yml
    satellites_doppler_correction.block.yml
    satellites_encode_rs.block.yml
    satellites_encode_rs_ccsds.block.yml
    satellites_eseo_line_decoder.block.yml
    satellites_eseo_packet_crop.block.yml
    satellites_fixedlen_tagger.block.yml
    satellites_fixedlen_to_pdu.block.yml
    satellites_funcube_submit.block.yml
    satellites_hdlc_deframer.block.yml
    satellites_hdlc_framer.block.yml
    satellites_k2sat_deframer.block.yml
    satellites_kiss_to_pdu.block.yml
    satellites_ks1q_header_remover.block.yml
    satellites_lilacsat1_demux.block.yml
    satellites_lilacsat1_gps_kml.block.yml
    satellites_manchester_sync.block.yml
    satellites_matrix_deinterleaver_soft.block.yml
    satellites_ngham_check_crc.block.yml
    satellites_ngham_packet_crop.block.yml
    satellites_ngham_remove_padding.block.yml
    satellites_nrzi_decode.block.yml
    satellites_nrzi_encode.block.yml
    satellites_nusat_decoder.block.yml
    satellites_pdu_add_meta.block.yml
    satellites_pdu_head_tail.block.yml
    satellites_pdu_length_filter.block.yml
    satellites_pdu_scrambler.block.yml
    satellites_pdu_to_kiss.block.yml
    satellites_phase_unwrap.block.yml
    satellites_print_header.block.yml
    satellites_print_timestamp.block.yml
    satellites_pwsat2_submitter.block.yml
    satellites_pwsat2_telemetry_parser.block.yml
    satellites_reflect_bytes.block.yml
    satellites_selector.block.yml
    satellites_snet_classifier.block.yml
    satellites_snet_deframer.block.yml
    satellites_submit.block.yml
    satellites_swap_crc.block.yml
    satellites_swap_header.block.yml
    satellites_swiatowid_packet_crop.block.yml
    satellites_swiatowid_packet_split.block.yml
    satellites_sx12xx_check_crc.block.yml
    satellites_sx12xx_packet_crop.block.yml
    satellites_u482c_decode.block.yml
    satellites_varlen_packet_framer.block.yml
    satellites_varlen_packet_tagger.block.yml
    satellites_viterbi_decoder.block.yml
    DESTINATION share/gnuradio/grc/blocks
)

add_subdirectory(ccsds)
add_subdirectory(components)
add_subdirectory(core)
add_subdirectory(hier)
add_subdirectory(usp)
