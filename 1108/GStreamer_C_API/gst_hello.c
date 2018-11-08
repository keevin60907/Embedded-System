#include<gst/gst.h>
#include<glib.h>

int main(int argc, char* argv[])
{
  gst_init(&argc, &argv);


  GstElement *pipe, *src, *sink;
  GMainLoop *loop;

  loop=g_main_loop_new(NULL,FALSE);

  
  // create pipeline

  pipe = gst_pipeline_new(NULL);

  // create elements

  src = gst_element_factory_make("v4l2src", NULL);
  sink = gst_element_factory_make("autovideosink", NULL);

  // check if initialize succeeded

  if(!(pipe && src && sink)){
    g_print("Fail to init factories!\n");
    return -1;
  }

  // set up the pipeline

  gst_bin_add_many(GST_BIN(pipe), src, sink, NULL);
  gst_element_link_many(src, sink, NULL);

  // set the pipeline to 'playing state'

  g_print("Playing");
  gst_element_set_state(pipe,GST_STATE_PLAYING);
  g_main_loop_run(loop);

  // clean up

  g_print("Clean up");
  gst_object_unref(GST_OBJECT(pipe));
  g_main_loop_unref(loop);
  
  return 0;
}
