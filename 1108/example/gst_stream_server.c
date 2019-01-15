#include<gst/gst.h>
#include<glib.h>
#include<signal.h>
#include<stdio.h>


GMainLoop *loop;


//It seems that no in-build ctrl-c handler in gstreamer
//so we have to use signal() function in <signal.h> to handle it.
//note that the *loop must be global to fit signal() function.
void ctrl_c_stop()
{
  g_print ("Ctrl-C pressed.\n");
  g_main_loop_quit(loop);
}

static gboolean bus_call(GstBus *bus, GstMessage *msg, gpointer data)
{
  GMainLoop *loop = (GMainLoop *) data;
  
  switch(GST_MESSAGE_TYPE(msg))
  {
    case GST_MESSAGE_EOS:
      g_print ("End of stream\n");
      g_main_loop_quit(loop);
      break;

    case GST_MESSAGE_ERROR:
    {
      gchar  *debug;
      GError *error;

      gst_message_parse_error(msg, &error, &debug);
      g_free(debug);

      g_printerr("Error: %s\n", error->message);
      g_error_free(error);

      g_main_loop_quit(loop);
      break;
    }

    default:
      break;
  }
}

int main(int argc, char* argv[])
{
  gst_init(&argc, &argv);


  GstElement *pipe, *src, *enc, *pay, *sink;
  GstBus     *bus;
  guint       bus_watch_id;

  loop=g_main_loop_new(NULL,FALSE);

  // create pipeline

  pipe = gst_pipeline_new(NULL);

  // create elements

  src = gst_element_factory_make("v4l2src", NULL);
  if (!src)
    fprintf(stderr,"src error!\n");
  
  // src = gst_element_factory_make("fdsrc", NULL);
  enc = gst_element_factory_make("x264enc", NULL);
  if (!enc)
    fprintf(stderr, "enc error!\n");
  pay = gst_element_factory_make("rtph264pay", NULL);
  if (!pay)
    fprintf(stderr, "pay error!\n");
  sink = gst_element_factory_make("udpsink", NULL);
  if (!sink)
    fprintf(stderr, "sink error!\n");
  
  // set elements properties

  g_object_set(sink, "host", "192.168.1.50", NULL);
  g_object_set(sink, "port", 5001, NULL);
  
  // tune=4 means zerolatency
  // for more information of x264enc params, please refer to:
  // http://fpvlab.com/forums/printthread.php?t=4869&pp=10&page=10
  g_object_set(enc, "tune", 4, NULL);

  // check if initialize succeeded

  if(!(pipe && src && enc && pay && sink)){
    g_print("Fail to init factories!\n");
    return -1;
  }

  // set up the pipeline

  gst_bin_add_many(GST_BIN(pipe), src, enc, pay, sink, NULL);
  gst_element_link_many(src, enc, pay, sink, NULL);

  // set up bus watch

  bus = gst_pipeline_get_bus(GST_PIPELINE(pipe));
  bus_watch_id = gst_bus_add_watch(bus, bus_call, loop);
  gst_object_unref(bus);

  signal(SIGINT, ctrl_c_stop);

  // set the pipeline to 'playing state'

  g_print("Playing\n");
  gst_element_set_state(pipe,GST_STATE_PLAYING);
  g_main_loop_run(loop);

  // clean up

  g_print("Cleaning up\n");
  gst_element_set_state(pipe,GST_STATE_NULL);
  gst_element_set_state(sink,GST_STATE_NULL);
  gst_object_unref(GST_OBJECT(pipe));
  g_main_loop_unref(loop);
  
  return 0;
}
